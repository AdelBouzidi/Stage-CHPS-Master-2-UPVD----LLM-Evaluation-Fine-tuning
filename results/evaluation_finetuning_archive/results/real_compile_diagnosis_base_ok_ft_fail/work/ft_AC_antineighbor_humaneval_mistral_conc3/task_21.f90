program rescale_to_unit_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  integer :: i

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Call the function
  call rescale_to_unit(numbers_len, numbers, res)

  ! Output result
  print *, 'Rescaled values:'
  do i = 1, numbers_len
    print *, res(i)
  end do

contains

  subroutine rescale_to_unit(numbers_len, numbers, res)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: res(numbers_len)
    real(dp) :: min_val, max_val, range

    min_val = numbers(1)
    do i = 2, numbers_len
      if (numbers(i) < min_val) min_val = numbers(i)
    end do

    max_val = numbers(1)
    do i = 2, numbers_len
      if (numbers(i) > max_val) max_val = numbers(i)
    end do

    range = max_val - min_val
    if (range == 0.0_dp) then
      res = 0.0_dp
    else
      res = (numbers - min_val) / range
    end if
  end subroutine rescale_to_unit

end program rescale_to_unit_demo