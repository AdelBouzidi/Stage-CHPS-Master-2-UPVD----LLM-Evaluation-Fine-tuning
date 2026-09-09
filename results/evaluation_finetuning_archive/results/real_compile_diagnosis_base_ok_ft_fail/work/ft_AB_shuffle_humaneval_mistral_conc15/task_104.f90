program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, n

  ! Hardcoded input as per example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, 'Result:', result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, n, temp
    integer :: digits(10)
    integer :: num, digit

    ! Initialize result array
    allocate(res(x_len))
    n = 0
    do i = 1, x_len
      num = x(i)
      digits = 0
      do while (num > 0)
        digit = mod(num, 10)
        if (mod(digit, 2) == 0) then
          digits(digit) = 1
        end if
        num = num / 10
      end do
      if (all(digits == 0)) then
        n = n + 1
        res(n) = x(i)
      end if
    end do

    ! Sort the result array
    call sort_array(res, n)

    ! Resize the result array to the correct size
    if (allocated(res)) deallocate(res)
    allocate(res(n))
    res = res(1:n)

  end function unique_digits

  subroutine sort_array(arr, n)
    implicit none
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

end program main