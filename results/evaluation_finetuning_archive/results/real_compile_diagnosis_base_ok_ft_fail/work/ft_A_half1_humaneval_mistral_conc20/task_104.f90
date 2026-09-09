program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, j, n, temp, digit

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) (x(i), i=1,x_len)

  ! Call the function
  call unique_digits(x_len, x, result)

  ! Output result
  if (allocated(result)) then
    write(*,*) (result(i), i=1,size(result))
  else
    write(*,*) 0
  end if

contains

  subroutine unique_digits(x_len, x, result)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(*)
    integer, allocatable, intent(out) :: result(:)
    integer :: i, j, n, temp, digit
    logical :: has_even

    ! Initialize result array
    allocate(result(x_len))
    n = 0

    do i = 1, x_len
      has_even = .false.
      temp = x(i)
      do while (temp > 0)
        digit = mod(temp, 10)
        temp = temp / 10
        if (mod(digit, 2) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        n = n + 1
        result(n) = x(i)
      end if
    end do

    ! Sort the result array
    do i = 1, n-1
      do j = i+1, n
        if (result(i) > result(j)) then
          temp = result(i)
          result(i) = result(j)
          result(j) = temp
        end if
      end do
    end do
  end subroutine unique_digits

end program main