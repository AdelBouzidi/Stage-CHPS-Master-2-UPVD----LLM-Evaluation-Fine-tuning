program rescale_to_unit_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: result(:)
  integer :: i

  ! Hardcoded input data
  numbers_len = 5
  allocate(numbers(numbers_len))
  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]

  ! Call the function
  result = rescale_to_unit(numbers_len, numbers)

  ! Output the result
  print *, 'Result:'
  do i = 1, size(result)
    print *, result(i)
  end do

contains

  function rescale_to_unit(numbers_len, numbers) result(res)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), allocatable :: res(:)
    real(dp) :: min_val, max_val
    integer :: i

    allocate(res(numbers_len))
    min_val = minval(numbers)
    max_val = maxval(numbers)
    
    if (max_val == min_val) then
      res = 0.0_dp
    else
      do i = 1, numbers_len
        res(i) = (numbers(i) - min_val) / (max_val - min_val)
      end do
    end if
  end function rescale_to_unit

end program rescale_to_unit_demo