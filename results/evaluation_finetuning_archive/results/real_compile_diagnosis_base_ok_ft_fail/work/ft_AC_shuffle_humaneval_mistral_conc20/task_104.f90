program unique_digits_demo
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, n

  ! Hardcoded input for demonstration
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  call unique_digits(x_len, x, result)

  print *, 'Result:', result

contains

  subroutine unique_digits(x_len, x, result)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(*)
    integer, allocatable, intent(out) :: result(:)
    integer :: i, n, temp
    integer :: digits(10)
    integer :: num, digit

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
      if (sum(digits) == 0) then
        n = n + 1
      end if
    end do

    allocate(result(n))
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
      if (sum(digits) == 0) then
        n = n + 1
        result(n) = x(i)
      end if
    end do

    call sort(result, n)
  end subroutine unique_digits

  subroutine sort(arr, n)
    implicit none
    integer, intent(inout) :: arr(*)
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
  end subroutine sort

end program unique_digits_demo