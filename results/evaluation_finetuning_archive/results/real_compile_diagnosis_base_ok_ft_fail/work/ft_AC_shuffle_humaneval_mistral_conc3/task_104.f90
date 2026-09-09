program unique_digits
  implicit none
  integer, allocatable :: x(:)
  integer :: x_len
  integer, allocatable :: result(:)
  integer :: i, j, n, idx
  integer :: temp

  ! Read input
  read(*,*) x_len
  read(*,*) x

  ! Initialize result array
  allocate(result(x_len))
  n = 0

  ! Filter numbers that don't contain even digits
  do i = 1, x_len
    if (has_no_even_digit(x(i))) then
      n = n + 1
      result(n) = x(i)
    end if
  end do

  ! Sort the result array
  call sort_array(result, n)

  ! Output the result
  write(*,*) result(1:n)

contains

  logical function has_no_even_digit(num)
    integer, intent(in) :: num
    integer :: digit
    has_no_even_digit = .true.
    do while (num > 0)
      digit = mod(num, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        has_no_even_digit = .false.
        return
      end if
      num = num / 10
    end do
  end function has_no_even_digit

  subroutine sort_array(arr, n)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    do i = 1, n-1
      do j = i+1, n
        if (arr(j) < arr(i)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program unique_digits